import Api from "./Api"
import UserService from "./UserService"

class AuthService {

    user = null

    isAuthenticated() {
        return this.user != null
    }

    async login(email, password) {
        const response = await Api.post("/api/auth/login", { email, password })
        if (!response.token) throw "Token não disponível"
        Api.setToken(response.token)
        sessionStorage.setItem("token", response.token)
        var user = await UserService.getUserByEmail(email)
        if (!user) throw "Usuário inválido"
        this.user = user
        return user
    }

    async getCurrentUser() {
        this.user = null
        let token = sessionStorage.getItem("token")
        if (token) {
            Api.setToken(token)
            const response = await Api.get("/api/auth/user")
            this.user = response
        }
        return this.user
    }

    logout() {
        sessionStorage.removeItem("token")
        this.user = null
    }
}

export default new AuthService()