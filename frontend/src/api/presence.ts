const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function post<TResponse>(path: string, payload: unknown): Promise<TResponse> {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data?.detail ?? "Request failed");
  }

  return data as TResponse;
}

export function getDeviceSwapDate(phoneNumber: string) {
  return post("/nac/device-swap/date", { phone_number: phoneNumber });
}

export function checkDeviceSwap(phoneNumber: string, maxAgeHours?: number) {
  return post("/nac/device-swap/check", {
    phone_number: phoneNumber,
    max_age_hours: maxAgeHours,
  });
}

export function kycFillIn(phoneNumber: string) {
  return post("/nac/kyc/fill-in", { phone_number: phoneNumber });
}
