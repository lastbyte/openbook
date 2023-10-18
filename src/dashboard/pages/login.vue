<template class="w-100 h-100">
    <b-container
        fluid
        class="p-5 h-100 w-100 d-flex justify-content-between align-items-center"
        :style="{
            background: 'url(' + bg + ')',
            backgroundPosition: 'center',
            backgroundSize: 'contain',
            backgroundRepeat: 'no-repeat',
        }"
    >
        <h1>OpenBook</h1>
        <b-form class="p-4" @submit="userLogin">
            <b-alert
                :show="dismissCountDown"
                dismissible
                variant="danger"
                @dismissed="dismissCountDown = 0"
                @dismiss-count-down="countDownChanged"
            >
                <p>Invalid email or password !!</p>
            </b-alert>
            <label class="sr-only my-3" for="form-input-username">username</label>
            <b-input-group prepend="@" class="my-3 mr-sm-2 mb-sm-0">
                <b-form-input
                    size="lg"
                    style="width: 350px"
                    v-model="username"
                    id="form-input-username"
                    placeholder="username"
                    required
                ></b-form-input>
            </b-input-group>

            <label class="sr-only my-3" for="form-input-password">Password</label>
            <b-input-group prepend="#" class="my-3 mr-sm-2 mb-sm-0">
                <b-form-input
                    style="width: 350px"
                    size="lg"
                    v-model="password"
                    id="form-input-password"
                    type="password"
                    placeholder="password"
                    required
                    @keydown.enter.prevent="userLogin"
                ></b-form-input>
            </b-input-group>

            <b-button @click="userLogin" class="px-4 py-2 my-3 d-flex align-items-center" variant="primary"
                >Login</b-button
            >
        </b-form>
    </b-container>
</template>

<script>
import background from '@/assets/images/bg.png';

export default {
    data() {
        return { bg: background, dismissSecs: 5, dismissCountDown: 0 };
    },
    created() {
        if (this.$auth.loggedIn) {
            this.$router.push('/');
        }
    },
    methods: {
        showAlert() {
            this.dismissCountDown = this.dismissSecs;
        },
        async userLogin(e) {
            try {
                e.preventDefault();
                const response = await this.$auth.loginWith('local', {
                    data: `username=${this.username}&password=${this.password}`,
                });
                localStorage.setItem('_auth_token', response.token);
                this.$router.push('/');
            } catch (err) {
                this.showAlert();
                console.log(err);
            }
        },
    },
};
</script>
