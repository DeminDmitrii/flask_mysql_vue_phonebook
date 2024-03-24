<template>
    <div class="container">
        <h1 class="text-center mb-4">Телефонная книга</h1>
        <contact-adding-form @add="addContact" ref="form"></contact-adding-form>
        <filter-form @filter="searchContacts"></filter-form>
        <div class="table-responsive-lg row mt-3">
            <table class="table table-hover">
                <thead>
                <tr>
                    <th>№</th>
                    <th>Имя</th>
                    <th>Фамилия</th>
                    <th>Номер телефона</th>
                    <th></th>
                    <th>
                        <input type="checkbox" v-model="selectAll">
                    </th>
                </tr>
                </thead>
                <tbody v-for="(contact, index) in contacts" :key="contact.id">
                <tr>
                    <td>{{ index + 1 }}</td>
                    <td>{{ contact.name }}</td>
                    <td>{{ contact.surname }}</td>
                    <td>{{ contact.phone }}</td>
                    <td>
                        <button type="button" class="btn btn-sm btn-warning me-3" @click="showEditModalDialog(contact)">
                            Редактировать
                        </button>
                        <button type="button" class="btn btn-sm btn-danger mt-1 mt-md-0"
                                @click="showDeleteModalDialog([contact.id])">
                            Удалить
                        </button>
                    </td>
                    <td>
                        <input type="checkbox" :value="contact.id" v-model="selectedContactsIds">
                    </td>
                </tr>
                </tbody>
            </table>
            <div class="row">
                <div>
                    <button class="btn btn-danger float-end col-auto"
                            @click="showDeleteModalDialog(selectedContactsIds)">
                        Удалить
                    </button>
                </div>
            </div>
        </div>
    </div>

    <delete-modal-dialog ref="deleteConfirmModalDialog" @deleteContacts="deleteContacts"></delete-modal-dialog>

    <edit-modal-dialog :editedContact="editedContact"
                       ref="editConfirmModalDialog"
                       @save="saveContact">
    </edit-modal-dialog>

    <validation-error-dialog ref="validationErrorDialog">
        <template #validationErrorMessage>{{ validationErrorMessage }}</template>
    </validation-error-dialog>
</template>

<script>
import ContactAddingForm from "./ContactAddingForm.vue";
import FilterForm from "./FilterForm.vue";
import PhoneBookService from "./PhoneBookService";
import ValidationErrorDialog from "./ValidationErrorDialog.vue";
import DeleteModalDialog from "./DeleteModalDialog.vue";
import EditModalDialog from "./EditModalDialog.vue";


export default {
    name: "App",

    components: {
        ContactAddingForm,
        FilterForm,
        DeleteModalDialog,
        EditModalDialog,
        ValidationErrorDialog
    },

    data() {
        return {
            contacts: [],
            selectedContactsIds: [],
            selectAll: false,
            service: new PhoneBookService(),
            editedContact: null,
            deletedContacts: null,
            validationErrorMessage: "",
            term: ""
        };
    },

    created() {
        this.loadContacts();
    },

    watch: {
        selectAll(newSelectAll) {
            if (newSelectAll) {
                this.selectedContactsIds = this.contacts.map(contact => contact.id);
            } else {
                this.selectedContactsIds = [];
            }
        }
    },

    methods: {
        showErrorMessageDialog(errorMessage) {
            this.validationErrorMessage = errorMessage;
            this.$refs.validationErrorDialog.show();
        },

        addContact(contact) {
            this.service.addContact(contact).then(response => {
                if (!response.data.success) {
                    this.showErrorMessageDialog(response.data.message);
                } else {
                    this.loadContacts();
                    this.$refs.form.clear();
                }
            }).catch(() => {
                this.showErrorMessageDialog("Ошибка добавления контакта");
            });
        },

        showDeleteModalDialog(deletedContacts) {
            this.deletedContacts = this.contacts
                .filter(contact => deletedContacts.includes(contact.id))
                .map(contact => contact.id);

            this.$refs.deleteConfirmModalDialog.show();
        },

        showEditModalDialog(contact) {
            this.editedContact = contact;
            this.$refs.editConfirmModalDialog.show();
        },

        saveContact(contactToSave) {
            this.service.updateContact(contactToSave).then(response => {
                if (!response.data.success) {
                    this.showErrorMessageDialog(response.data.message);
                } else {
                    this.loadContacts();
                    this.$refs.editConfirmModalDialog.hide();
                }
            }).catch(() => {
                    this.showErrorMessageDialog("Ошибка добавления контакта");
            });
        },

        deleteContacts() {
            this.service.deleteContacts(this.deletedContacts).then(() => {
                this.selectedContactsIds = this.selectedContactsIds
                    .filter(id => !this.deletedContacts.includes(id));
                this.selectAll = false;

                this.$refs.deleteConfirmModalDialog.hide();
                this.loadContacts();
            }).catch(() => {
                this.showErrorMessageDialog("Ошибка добавления контакта");
            });
        },

        searchContacts(term) {
            this.term = term;
            this.loadContacts();
        },

        loadContacts() {
            this.service.getContacts(this.term).then(contacts => {
                this.contacts = contacts.data;
            }).catch(() => {
                this.showErrorMessageDialog("Ошибка загрузки контактов");
            });
        }
    }
};
</script>
