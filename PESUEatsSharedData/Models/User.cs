using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace PESUEatsSharedData.Models
{
    public class User
	{
		[JsonPropertyName("username")]
		public string username { get; set; }

		[JsonPropertyName("password")]
		public string password { get; set; }

		[JsonPropertyName("roles")]
		public string[] roles { get; set; }

		public User(string username, string password, string[] roles)
		{
			this.username = username;
			this.password = password;
			this.roles = roles;
		}
    }
}
