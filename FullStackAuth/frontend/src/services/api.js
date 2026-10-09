
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function apiRequest(
  path,
  options = {},
  auth = {}
) {
  const {
    accessToken,
    headers: customHeaders = {},
    ...requestOptions
  } = options;

  const headers = { ...customHeaders };

  if (requestOptions.body && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  function sendRequest(token) {
    const requestHeaders = { ...headers };

    if (token) {
      requestHeaders.Authorization = `Bearer ${token}`;
    } else {
      delete requestHeaders.Authorization;
    }

    return fetch(`${API_BASE_URL}${path}`, {
      ...requestOptions,
      headers: requestHeaders,
      credentials: "include",
    });
  }

  let response = await sendRequest(accessToken);

  if (response.status !== 401 || !auth.updateAccessToken) {
    return parseResponse(response);
  }

  const refreshResponse = await fetch(
    `${API_BASE_URL}/api/v1/auth/refresh`,
    {
      method: "POST",
      credentials: "include",
    }
  );

  if (!refreshResponse.ok) {
    auth.logout?.();
    throw new Error("Your session expired. Please log in again.");
  }

  const refreshData = await refreshResponse.json();

  if (!refreshData.access_token) {
    auth.logout?.();
    throw new Error("Refresh response did not contain an access token.");
  }

  auth.updateAccessToken(refreshData.access_token);

  // Retry the original request only once.
  response = await sendRequest(refreshData.access_token);

  if (response.status === 401) {
    auth.logout?.();
    throw new Error("Your session expired. Please log in again.");
  }

  return parseResponse(response);
}

async function parseResponse(response) {
  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(
      data?.detail || `Request failed with status ${response.status}`
    );
  }

  return data;
}
