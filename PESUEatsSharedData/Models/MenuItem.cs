using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace PESUEatsSharedData.Models
{
    public class MenuItem
    {
		[JsonPropertyName("Iid")]
		public int id { get; set; }

		[JsonPropertyName("IinMenuRid")]
		public int inMenuRid { get; set; }

		[JsonPropertyName("IName")]
		public string name { get; set; }

		[JsonPropertyName("IPrice")]
		public float price { get; set; }

		[JsonPropertyName("IDescription")]
		public string? description { get; set; }

		[JsonPropertyName("ICategory")]
		public string? category { get; set; }

		public MenuItem(int id, int inMenuRid, string name, float price, string? description, string? category)
		{
			this.id = id;
			this.inMenuRid = inMenuRid;
			this.name = name;
			this.price = price;
			this.description = description;
			this.category = category;
		}
	}
}
