import axios from "axios";

export default class PhoneBookService {
    constructor() {
        this.baseUrl = "http://127.0.0.1:5000/api/contacts";
    }

    getContacts(term) {
        return axios.get(this.baseUrl, {params: {term}}).then(response => response.data);
    }

    deleteContacts(ids) {
        const queryString = new URLSearchParams();
        ids.forEach(id => queryString.append("id", id));

        return axios.delete(`${this.baseUrl}/?${queryString}`).then(response => response.data);
    }

    addContact(contact) {
        return axios.post(this.baseUrl, contact);
    }

    updateContact(contact) {
        return axios.put(this.baseUrl, contact).then(response => response.data);
    }
}
