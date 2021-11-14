using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace PESUEatsSharedData.Models
{
    public class MenuItemInCart
    {
		[JsonPropertyName("MIid")]
		public int id { get; set; }

		[JsonPropertyName("MICartId")]
		public int CartId { get; set; }

		[JsonPropertyName("MICartCustId")]
		public int CartCustId { get; set; }

		[JsonPropertyName("MIQuantity")]
		public int Quantity { get; set; }

		public MenuItemInCart(int id, int CartId, int CartCustId, int Quantity)
		{
			this.id = id;
			this.CartId = CartId;
			this.CartCustId = CartCustId;
			this.Quantity = Quantity;
		}
	}
}
