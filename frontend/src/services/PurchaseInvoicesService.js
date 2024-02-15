import Api from "./Api";

class PurchaseInvoicesService {

    async addPurchaseInvoice(purchaseInvoice) {
        return await Api.post("/api/purchase_invoices", purchaseInvoice)
    }

    async updatePurchaseInvoice(purchaseInvoice) {
        return await Api.patch("/api/purchase_invoices/" + purchaseInvoice.id, purchaseInvoice)
    }

    async deletePurchaseInvoice(purchaseInvoiceId) {
        await Api.delete("/api/purchase_invoices/" + purchaseInvoiceId)
    }

    async getPurchaseInvoicesSummary(column, filters) {
        return await Api.get("/api/purchase_invoices/summary/" + column, filters)
    }

    async getPurchaseInvoices(filters) {
        return await Api.get("/api/purchase_invoices", filters)
    }

    async getPurchaseInvoiceById(purchaseInvoiceId) {
        return await Api.get("/api/purchase_invoices/" + purchaseInvoiceId)
    }
}

export default new PurchaseInvoicesService()