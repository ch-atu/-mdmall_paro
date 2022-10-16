import store from "@/store";
import {getUser} from "@/api/user.request";

export function canTo(to_path, token, next){
    if (store.state.user.username) {
        next()
    } else if (token) {
        getUser().then(res => {
            res.data.token = token;
            console.log('获取用户信息', res);
            store.commit('user/SAVE_USER', res.data);
            next()
        }).catch(err => {
            to_path ? next(to_path) : next()
            // next({name: 'Login'})
        })
    } else {
        // next({name: 'Login'})
        to_path ? next(to_path) : next()
    }
}

