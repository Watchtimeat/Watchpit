import Api from "./Api";

class PurchaseOrdersService {
  async addPurchaseOrder(purchaseOrder) {
    return await Api.post("/api/purchase_orders", purchaseOrder);
  }

  async addPurchaseOrderByOs(purchaseOrder) {
    return await Api.post("/api/estoklus/order_by_so", purchaseOrder);
  }
  async addPurchaseOrderByPlanner(purchaseOrder) {
    return await Api.post("/api/purchase_orders/order_by_planner", purchaseOrder);
  }

  async updatePurchaseOrder(purchaseOrder) {
    return await Api.patch(
      "/api/purchase_orders/" + purchaseOrder.id,
      purchaseOrder
    );
  }

  async deletePurchaseOrder(purchaseOrderId) {
    await Api.delete("/api/purchase_orders/" + purchaseOrderId);
  }

  async getPurchaseOrdersSummary(column, filters) {
    return await Api.get("/api/purchase_orders/summary/" + column, filters);
  }

  async getPurchaseOrders(filters) {
    return await Api.get("/api/purchase_orders", filters);
  }

  async getPurchaseInvoiceOrders(filters) {
    return await Api.get(
      `/api/purchase_orders?status=confirmed&status=receiving&status=requested&brand=${filters.brand}`
    );
  }

  async getPurchaseOrderById(purchaseOrderId) {
    return await Api.get("/api/purchase_orders/" + purchaseOrderId);
  }

  async getPurchaseOrderInvoiceById(purchaseOrderId) {
    return await Api.get(`/api/purchase_orders/${purchaseOrderId}/invoice`);
  }

  async getBrandListOsOrderAvaiable() {
    return await Api.get("/api/estoklus/brands_by_so");
  }

  async uploadFiles(file) {
    return await Api.post("/api/resources", file);
  }

  async getUploadFiles(proformaId) {
    return await Api.get(`/api/resources/${proformaId}/stream`);
  }

  async ImportExcel(file, purchaseOrderId) {
    return await Api.post(
      `/api/purchase_orders/${purchaseOrderId}/import_excel`,
      file
    );
  }
}

export default new PurchaseOrdersService();
