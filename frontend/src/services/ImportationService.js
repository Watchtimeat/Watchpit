import Api from "./Api";

class ImportationService {
    async insertImportation(formData) {
        return await Api.post("/api/estoklus/importation",formData)
    }
}
export default new ImportationService()