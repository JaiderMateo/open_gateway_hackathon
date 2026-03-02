import { useState } from "react";
import { checkDeviceSwap, getDeviceSwapDate, kycFillIn } from "../api/presence";

export function PresenceCheck() {
  const [phoneNumber, setPhoneNumber] = useState("+99999991000");
  const [result, setResult] = useState<unknown>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const run = async (task: () => Promise<unknown>) => {
    setLoading(true);
    setError(null);
    try {
      const data = await task();
      setResult(data);
    } catch (err) {
      setResult(null);
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>PresenceCheck</h1>
      <p>Validate device history and retrieve customer KYC information.</p>

      <div className="form-row">
        <input
          value={phoneNumber}
          onChange={(event) => setPhoneNumber(event.target.value)}
          placeholder="E.164 format, e.g. +34900111222"
        />
      </div>

      <div className="actions">
        <button disabled={loading} onClick={() => run(() => getDeviceSwapDate(phoneNumber))}>
          Device Swap Date
        </button>
        <button disabled={loading} onClick={() => run(() => checkDeviceSwap(phoneNumber))}>
          Device Swap Check
        </button>
        <button disabled={loading} onClick={() => run(() => kycFillIn(phoneNumber))}>
          KYC Fill-in
        </button>
      </div>

      {error ? <pre>{JSON.stringify({ error }, null, 2)}</pre> : null}
      {result ? <pre>{JSON.stringify(result, null, 2)}</pre> : null}
    </div>
  );
}
