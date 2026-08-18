// Central configuration supporting both build-time and runtime values.
// At build time `import.meta.env.VITE_API_URL` is used. At runtime a
// `appsettings.json` file served from the `public/` folder can override values
// without rebuilding the app (useful for hosting environments).
export const config = {
  API_URL: import.meta.env.VITE_API_URL
}

export async function loadConfig() {
  try {
    const resp = await fetch('/appsettings.json', { cache: 'no-store' })
    if (!resp.ok) return
    const json = await resp.json()
    if (json && json.API_URL) {
      let url = String(json.API_URL).replace(/\s+/g, '').replace(/\/+$/g, '')
      if (!url.endsWith('/api/v1')) url = url + '/api/v1'
      config.API_URL = url
    }
  } catch (e) {
    // ignore and keep defaults
  }
}

export default config
