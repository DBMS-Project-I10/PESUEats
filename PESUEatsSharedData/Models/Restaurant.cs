using System.Text.Json.Serialization;

namespace PESUEatsSharedData.Models
{
	public class Restaurant
	{		
		[JsonPropertyName("Rid")]
		public int id { get; set; }
	
		[JsonPropertyName("RhasWid")]
		public int walletid { get; set; }

		[JsonPropertyName("RName")]
		public string name { get; set; }
		
		[JsonPropertyName("RLocation")]
		public string location { get; set; }
		
		[JsonPropertyName("RRating")]
		public float? rating { get; set; }
		
		[JsonPropertyName("RCuisine")]
		public string? cuisine { get; set; }

		public Restaurant(int id, int walletid, string name, string location, float? rating, string? cuisine)
		{
			this.id = id;
			this.walletid = walletid;
			this.name = name;
			this.location = location;
			this.rating = rating;
			this.cuisine = cuisine;
		}
	}
}
