export class APIError extends Error {
  constructor(
    public status: number,
    public message: string,
    public details?: any,
  ) {
    super(message);
  }
}

export const handleAPIError = (error: any): string => {
  if (error.response?.data?.message) {
    return error.response.data.message;
  }
  if (error.message === "Network Error") {
    return "Network error. Please check your connection.";
  }
  if (error.code === "ECONNABORTED") {
    return "Request timeout. Please try again.";
  }
  return "Something went wrong. Please try again later.";
};
