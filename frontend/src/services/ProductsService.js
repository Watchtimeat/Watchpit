import Api from "./Api";

class ProductsService {
  async addProduct(product) {
    return await Api.post("/api/products", product);
  }

  async updateProduct(product) {
    return await Api.patch("/api/products/" + product.id, product);
  }

  async deleteProduct(productId) {
    await Api.delete("/api/products/" + productId);
  }

  async getProducts(filters) {
    return await Api.get("/api/products", filters);
  }

  async getProductById(productId) {
    return await Api.get(`/api/products?id=${productId}`);
  }
}

export default new ProductsService();
