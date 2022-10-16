export default {
    namespaced: true,
    state: {
        token: '',
        avatar: '',
        mobile: '',
        user_id: '',
        username: '',
        email:'',
        email_active:'',
    },
    actions: {},
    mutations: {
        SAVE_USER(state, value) {
            state.token = value.token
            state.mobile = value.mobile
            state.user_id = value.id
            state.username = value.username
            state.email = value.email
            state.email_active = value.email_active
        },
        CLEAR(state, value){
            // console.log(state);
            for (let i in state){
                state[i] = ''
            }
        }
    },
    getters: {},
}


























