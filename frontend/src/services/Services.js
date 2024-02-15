import Api from "./Api";

class OrdersServicesService {
  
    async getServiceOrders_estoklus() {
      return await Api.get("/api/estoklus/service_orders");
    }
    
    async getServicesSummary(column, filters){
      return await Api.get("/api/service_orders/summary/" + column, filters);
    }
    async getServices(filters) {
      return await Api.get("/api/service_orders", filters);
    }
    async getCustomers(filters) {
      return await Api.get("/api/customers", filters);
    }
    async getGrupos(grupo) {
      return await Api.get("/api/estoklus/grupo/"+ grupo);
    }
    async addOS(service_order) {
      return await Api.post("/api/service_orders", service_order);
    }
    async addCustomer(customer) {
      return await Api.post("/api/customers", customer);
    }
    async updateCustomer(customer) {
      return await Api.patch("/api/customers/"+customer.cliente_id,customer);
    }
    async getUsersEstoklus() {
    return await Api.get("/api/estoklus/usuarios");
    }
    async getTrackingID(cliente_id) {
      return await Api.get("/api/estoklus/tracking/"+cliente_id);
      }
    async addEstimate(service_order) {
        return await Api.post("/api/service_orders/orcamento",service_order);
        }
    

  }
  
  export default new OrdersServicesService();