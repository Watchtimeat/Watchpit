import Api from "./Api";

class PartsConferenceService {
  async getPartsConference() {
    return await Api.get("/api/estoklus/gerar_separacao");
  }

  async generateRomaneio(data) {
    return await Api.post("/api/estoklus/gerar_romaneio", data);
  }
}

export default new PartsConferenceService();
