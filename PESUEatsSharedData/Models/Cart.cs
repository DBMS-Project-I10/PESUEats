using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace PESUEatsSharedData.Models
{
    public class Cart
    {
		[JsonPropertyName("CartId")]
		public int id { get; set; }

		[JsonPropertyName("CartCustId")]
		public int CartCustId { get; set; }

		[JsonPropertyName("CartStatus")]
		public string status { get; set; }

		[JsonPropertyName("CartTotalBillAmount")]
		public float? totalBillAmount { get; set; }

		[JsonPropertyName("CartTaxAmount")]
		public float? taxAmount { get; set; }

		[JsonPropertyName("CartDeliveryAmount")]
		public float? deliveryAmount { get; set; }

		public Cart(int id, int CartCustId, string status, float? totalBillAmount, float? taxAmount, float? deliveryAmount)
		{
			this.id = id;
			this.CartCustId = CartCustId;
			this.status = status;
			this.totalBillAmount = totalBillAmount;
			this.taxAmount = taxAmount;
			this.deliveryAmount = deliveryAmount;
		}
	}
}
