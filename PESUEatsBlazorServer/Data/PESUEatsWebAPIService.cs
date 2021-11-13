using PESUEatsSharedData.Models;
using System.Text.Json;

namespace PESUEatsBlazorServer.Data
{
    public class PESUEatsWebAPIService
    {
        private readonly HttpClient client;

        public PESUEatsWebAPIService(HttpClient client)
        {
            this.client = client;
        }

        public async Task<List<Restaurant>> GetRestaurantsAsync()
        {
            var response = await client.GetAsync("ls/restaurants");
            response.EnsureSuccessStatusCode();

            using var responseContent = await response.Content.ReadAsStreamAsync();
            return await JsonSerializer.DeserializeAsync<List<Restaurant>>(responseContent);
        }
    }
}
