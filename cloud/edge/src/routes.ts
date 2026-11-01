// Route classification for the login wall (Spec 083, FR-004 as
// strengthened by Amendment 2).
//
// The anonymous (unauthenticated) surface is EXACTLY:
//   - /robots.txt            (served by the edge itself)
//   - /login, /setup, /invite/*   (public pages)
//   - the SPA shell's static assets (they carry no project data)
// Everything else is gated: anonymous API requests answer 401 and
// anonymous page requests redirect to /login.

export type RouteClass =
  | "robots"
  | "public-page"
  | "public-asset"
  | "api"
  | "page";

const PUBLIC_PAGE_PATHS = new Set(["/login", "/setup", "/invite"]);

/**
 * Static-asset extensions for the SPA shell. Deliberately a closed
 * list: a path whose extension is not listed here is treated as a page
 * (gated), never as a public asset. Data formats (json, csv, zip, …)
 * are NOT assets — content-bearing payloads are never public.
 */
const STATIC_ASSET_EXTENSIONS = new Set([
  "js",
  "mjs",
  "css",
  "map",
  "svg",
  "png",
  "jpg",
  "jpeg",
  "gif",
  "webp",
  "avif",
  "ico",
  "woff",
  "woff2",
  "ttf",
  "otf",
  "webmanifest",
]);

export function isPublicPage(pathname: string): boolean {
  return PUBLIC_PAGE_PATHS.has(pathname) || pathname.startsWith("/invite/");
}

export function isStaticAsset(pathname: string): boolean {
  if (pathname.startsWith("/assets/")) return true;
  const dot = pathname.lastIndexOf(".");
  if (dot <= pathname.lastIndexOf("/")) return false;
  return STATIC_ASSET_EXTENSIONS.has(pathname.slice(dot + 1).toLowerCase());
}

export function classifyRoute(pathname: string): RouteClass {
  if (pathname === "/robots.txt") return "robots";
  if (pathname === "/api" || pathname.startsWith("/api/")) return "api";
  if (isPublicPage(pathname)) return "public-page";
  if (isStaticAsset(pathname)) return "public-asset";
  return "page";
}

/** Strip trailing slashes (except the root) before classification. */
export function normalizePathname(pathname: string): string {
  if (pathname.length > 1) return pathname.replace(/\/+$/, "");
  return pathname;
}
