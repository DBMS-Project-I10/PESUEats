using System.Text.Json.Serialization;

namespace PESUEatsSharedData.Models
{
	public class Restaurant
	{
		[JsonPropertyName("ssn")]
		public int Ssn { get; set; }

		[JsonPropertyName("pno")]
		public int ProjectNumber { get; set; }

		[JsonPropertyName("hours")]
		public float Hours { get; set; }

		public Restaurant(int Ssn, int ProjectNumber, float Hours)
		{
			this.Ssn = Ssn;
			this.ProjectNumber = ProjectNumber;
			this.Hours = Hours;
		}
	}
}
