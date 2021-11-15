using PESUEatsSharedData.Models;
using System.Text.Json;

namespace PESUEatsBlazorServer.Services
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
            var response = await client.GetAsync("restaurants");
            //response.EnsureSuccessStatusCode();

            using var responseContent = await response.Content.ReadAsStreamAsync();
            return await JsonSerializer.DeserializeAsync<List<Restaurant>>(responseContent);
        }

        public async Task<List<User>>? GetUsersAsync(string? username)
        {
            User admin = new User("Admin", "1234", new[] { "" });
            HttpResponseMessage response;
            if (username == null)
                response = await client.PostAsJsonAsync("users", admin);
            else
                response = await client.PostAsJsonAsync($"users/{username.ToLower()}", admin);

            if (response.IsSuccessStatusCode)
            {
                using var responseContent = await response.Content.ReadAsStreamAsync();
                return await JsonSerializer.DeserializeAsync<List<User>>(responseContent);
            }
            else
            {
                return null;
            }
        }

        public async Task<bool>? Signup(User user)
        {
            User AuthUser = new User("Admin", "1234", new[] { "" });
            Tuple<User, User> tupleUser = new Tuple<User, User>(AuthUser, user);
            HttpResponseMessage response = await client.PostAsJsonAsync("signup", tupleUser);

            if (response.IsSuccessStatusCode)
            {
                return true;
            }
            else
            {
                return false;
            }
        }
    }
}
