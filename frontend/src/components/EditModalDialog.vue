<template>
    <div ref="modal" class="modal fade" data-bs-backdrop="static" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Редактировать контакт</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div>
                        <label for="name" class="form-label">Имя</label>
                        <input type="text"
                               id="name"
                               class="form-control"
                               v-model.trim="name"
                               :class="nameValidationClass"
                               required>
                        <div class="invalid-feedback">Введите имя</div>
                    </div>
                    <div>
                        <label for="surname" class="form-label">Фамилия</label>
                        <input type="text"
                               id="surname"
                               class="form-control"
                               v-model.trim="surname"
                               :class="surnameValidationClass"
                               required>
                        <div class="invalid-feedback">Введите фамилию</div>
                    </div>
                    <div>
                        <label for="phone-number" class="form-label">Номер телефона</label>
                        <input type="text"
                               id="phone-number"
                               class="form-control"
                               v-model.trim="phone"
                               :class="phoneValidationClass"
                               required>
                        <div class="invalid-feedback">Введите номер телефона</div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button @click="cancel" class="btn btn-secondary" data-bs-dismiss="modal">Отменить</button>
                    <button @click="save" class="btn btn-success">Сохранить</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {Modal} from "bootstrap";

export default {
    name: "EditModalDialog",

    emits: ["save"],

    props: {
        editedContact: Object,
        required: true
    },

    data() {
        return {
            modal: null,
            id: null,
            name: null,
            surname: null,
            phone: null
        };
    },

    mounted() {
        this.modal = new Modal(this.$refs.modal, {});
    },

    watch: {
        editedContact() {
            this.id = this.editedContact.id;
            this.name = this.editedContact.name;
            this.surname = this.editedContact.surname;
            this.phone = this.editedContact.phone;
        }
    },

    computed: {
        nameValidationClass() {
            return {
                "is-valid": this.name === null ? false : this.name.length !== 0,
                "is-invalid": this.name === null ? false : this.name.length === 0
            };
        },

        surnameValidationClass() {
            return {
                "is-valid": this.surname === null ? false : this.surname.length !== 0,
                "is-invalid": this.surname === null ? false : this.surname.length === 0
            };
        },

        phoneValidationClass() {
            return {
                "is-valid": this.phone === null ? false : this.phone.length !== 0,
                "is-invalid": this.phone === null ? false : this.phone.length === 0
            };
        }
    },

    methods: {
        show() {
            this.modal.show();
        },

        hide() {
            this.modal.hide();
        },

        cancel() {
            this.name = this.editedContact.name;
            this.surname = this.editedContact.surname;
            this.phone = this.editedContact.phone;
        },

        save() {
            if (this.nameValidationClass["is-valid"] && this.surnameValidationClass["is-valid"]
                && this.phoneValidationClass["is-valid"]) {
                const contactToSave = {
                    id: this.id,
                    name: this.name,
                    surname: this.surname,
                    phone: this.phone
                };

                this.$emit("save", contactToSave);
            }
        }
    }
};
</script>
