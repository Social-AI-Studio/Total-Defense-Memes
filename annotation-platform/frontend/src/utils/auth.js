import axios from 'axios';
import { Settings } from '../config/api.config';

export default {
    async login(user, pass, cb) {
        if (localStorage.token) {
            if (cb) cb(true)
            this.onChange(true)
            return
        }

        const body = new URLSearchParams({
            username: user,
            password: pass
        })

        const config = {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }

        const login = await axios.post(`${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/api/auth/signin`,
            body.toString(), config
        ).catch(error => {
            console.log(error)
            if (cb) cb(false)
            this.onChange(false)
        });
        
        localStorage.token = login.data.accessToken;
        if (cb) cb(true)
        this.onChange(true)
    },

    getToken() {
        return localStorage.token
    },

    logout(cb) {
        delete localStorage.token
        if (cb) cb()
        this.onChange(false)
    },

    loggedIn() {
        return !!localStorage.token
    },

    onChange() { }
}