import { PRIMARY_SERVER_BASE_URL } from "./envHelper";

const buildApiRouteString = (baseUrl: string, navRoutes: string[]) => {
  const trimmedBaseUrl = baseUrl.replace(/\/+$/, "");
  const trimmedNavRoutes = navRoutes.map((route) =>
    route.replace(/^\/+/, "").replace(/\/+$/, ""),
  );
  return `${trimmedBaseUrl}/${trimmedNavRoutes.join("/")}`;
};

const getPrimaryServerRoute = (navRoutes: string[]) => {
  return buildApiRouteString(PRIMARY_SERVER_BASE_URL, navRoutes);
};

export { getPrimaryServerRoute };
