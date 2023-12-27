/**
 * Makes an asynchronous HTTP GET request.
 * @param url
 * @returns 
 */
export async function getAsync<TResponse>(url: string): Promise<TResponse> {
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error("Error getting game.");
    }

    return await response.json() as TResponse;
}
