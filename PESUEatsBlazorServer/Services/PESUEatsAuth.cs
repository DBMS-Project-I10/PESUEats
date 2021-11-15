using Microsoft.AspNetCore.Components.Authorization;
using PESUEatsSharedData.Models;
using System.Security.Claims;

namespace PESUEatsBlazorServer.Services
{
    public class PESUEatsAuthStateProvider : AuthenticationStateProvider
    {
        public override Task<AuthenticationState> GetAuthenticationStateAsync()
        {
            /*var usernameClaim = new Claim(ClaimTypes.Name, Username);*/
            var identity = new ClaimsIdentity(/*new[] { usernameClaim }, "PESUEatsPostgresAuth"*/);
            var user = new ClaimsPrincipal(identity);

            return Task.FromResult(new AuthenticationState(user));
        }

        public void LoginUser(User the_user)
        {
            List<Claim> claims = new List<Claim>();
            claims.Add( new Claim(ClaimTypes.Name, the_user.username) );
            foreach (string role in the_user.roles)
            {
                claims.Add( new Claim(ClaimTypes.Role, role) );
            }
            var identity = new ClaimsIdentity(claims, "PESUEatsPostgresAuth");
            var user = new ClaimsPrincipal(identity);

            NotifyAuthenticationStateChanged(Task.FromResult(new AuthenticationState(user)));
        }

        public void LogoutUser()
        {
            var identity = new ClaimsIdentity();
            var user = new ClaimsPrincipal(identity);

            NotifyAuthenticationStateChanged(Task.FromResult(new AuthenticationState(user)));
        }
    }
}
