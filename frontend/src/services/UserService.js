import Api from "./Api";

class UserService {

    async addUser(user) {
        return await Api.post("/api/users", user)
    }

    async updateUser(user) {
        return await Api.patch("/api/users/" + user.id, user)
    }

    async deleteUser(user) {
        await Api.delete("/api/users/" + user.id)
    }

    async getUsers(filters) {
        return await Api.get("/api/users?_order_a=name", filters)
    }

    async getUserById(UserId) {
        return await Api.get("/api/users/" + UserId)
    }

    async getUserByEmail(email) {
        return await Api.get("/api/users/" + email)
    }
}

export default new UserService()