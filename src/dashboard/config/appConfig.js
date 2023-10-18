module.exports = {

    services : {
        library : {
            base : "http://localhost:8000/api",
            timeout : 3000,
            apiKey : 'web-interface',
            endPoints : {
                CREATE_BOOK : { path : "/books", method : 'POST'},
                GET_BOOK_BY_ID : { path : "/books", method : 'GET'},
                GET_BOOKS : { path : "/books", method : 'GET'},
                UPDATE_BOOK : { path : "/books", method : 'PUT'},
                DELETE_BOOK :{ path : "/books", method : 'DELETE'},
                CREATE_AUTHOR : { path : "/authors", method : 'POST'},
                GET_AUTHOR_BY_ID : { path : "/authors", method : 'GET'},
                GET_AUTHORS : { path : "/authors", method : 'GET'},
                UPDATE_AUTHOR : { path : "/authors", method : 'PUT'},
                DELETE_AUTHOR :{ path : "/authors", method : 'DELETE'}

            }
        }
    }
}