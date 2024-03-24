<template>
    <form @submit.prevent="submit" novalidate>
        <div class="row">
            <div class="col-sm-4">
                <label for="name" class="form-label">Имя</label>
                <input type="text" id="name"
                       v-model.trim="name"
                       class="form-control"
                       :class="nameValidationClass"
                       required>
                <div class="invalid-feedback">
                    Введите имя
                </div>
            </div>
            <div class="col-sm-4">
                <label for="surname" class="form-label">Фамилия</label>
                <input type="text" id="surname"
                       v-model.trim="surname"
                       class="form-control"
                       :class="surnameValidationClass"
                       required>
                <div class="invalid-feedback">
                    Введите фамилию
                </div>
            </div>
            <div class="col-sm-4">
                <label for="phone" class="form-label">Номер телефона</label>
                <input type="tel" id="phone"
                       v-model.trim="phone"
                       class="form-control"
                       :class="phoneValidationClass"
                       required>
                <div class="invalid-feedback">Введите номер телефона</div>
            </div>
            <div>
                <button class="col-auto mt-3 float-end btn btn-primary">Добавить</button>
            </div>
        </div>
    </form>
</template>

<script>
export default {
    name: "ContactAddingForm",

    emits: ["add"],

    data() {
        return {
            name: "",
            surname: "",
            phone: "",
            isAddingAttempt: false
        };
    },

    computed: {
        nameValidationClass() {
            return {
                "is-valid": this.name.length !== 0,
                "is-invalid": this.isAddingAttempt && this.name.length === 0
            };
        },

        surnameValidationClass() {
            return {
                "is-valid": this.surname.length !== 0,
                "is-invalid": this.isAddingAttempt && this.surname.length === 0
            };
        },

        phoneValidationClass() {
            return {
                "is-valid": this.phone.length !== 0,
                "is-invalid": this.isAddingAttempt && this.phone.length === 0
            };
        }
    },

    methods: {
        clear() {
            this.name = "";
            this.surname = "";
            this.phone = "";
        },

        submit() {
            this.isAddingAttempt = this.name.length === 0 || this.surname.length === 0 || this.phone.length === 0;

            if (this.nameValidationClass["is-invalid"]
                || this.surnameValidationClass["is-invalid"]
                || this.phoneValidationClass["is-invalid"]) {
                return;
            }

            const contact = {
                name: this.name,
                surname: this.surname,
                phone: this.phone
            };

            this.$emit("add", contact);
        }
    }
};
</script>
