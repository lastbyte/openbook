import {
    ACTION_SET_BOOK_TABLE_DATA,
    ACTION_SET_BOOK_ROW_DATA_DETAILS,
    ACTION_SET_BOOK_AUTHOR_OPTIONS,
    ACTION_SET_BOOK_ROW_TO_UPDATE,
    ACTION_SET_BOOK_ADD,
    ACTION_SET_BOOK_UPDATE
} from '~/store-config/action.types';
import {
    MUTATION_SET_BOOK_TABLE_DATA,
    MUTATION_SET_BOOK_AUTHOR_OPTIONS,
    MUTATION_SET_BOOK_ROW_DATA_DETAILS,
    MUTATION_SET_BOOK_ROW_TO_UPDATE,
    MUTATION_SET_BOOK_ADD,
    MUTATION_SET_BOOK_UPDATE
} from '~/store-config/mutation.types';

export const state = () => ({
    authorOptions: [],
    bookTable: {
        items: [],
        totalRows: 0,
        filter: '',
        perPage : '10',
        currentPage : 1  
    },
    addBook : {
        id : null,
        name : '',
        year_published : null,
        description : '',
        url : '',
        authors : []
    },
    rowToUpdate : {},
    updateBook : {}
});

export const mutations = {
    [MUTATION_SET_BOOK_TABLE_DATA](state, values) {
        state.bookTable = {...state.bookTable, ...values}
    },
    [MUTATION_SET_BOOK_AUTHOR_OPTIONS](state, value) {
        state.authorOptions = value;
    },
    [MUTATION_SET_BOOK_ADD](state, value) {
        state.addBook = {...state.addBook, ...value}
    },
    [MUTATION_SET_BOOK_UPDATE](state, value) {
        state.updateBook = {...state.updateBook, ...value}
    },
    [MUTATION_SET_BOOK_ROW_TO_UPDATE](state, value) {
        state.rowToUpdate = { ...value };
    },
    [MUTATION_SET_BOOK_ROW_DATA_DETAILS](state, row) {
        row.toggleDetails();
        state.bookTable.items.splice(row.index, 1, row.item);
    },
};

export const actions = {
    [ACTION_SET_BOOK_TABLE_DATA]({ commit }, value) {
        commit(MUTATION_SET_BOOK_TABLE_DATA, value);
    },
    [ACTION_SET_BOOK_AUTHOR_OPTIONS]({ commit }, value) {
        commit(MUTATION_SET_BOOK_AUTHOR_OPTIONS, value);
    },
    [ACTION_SET_BOOK_ROW_DATA_DETAILS]({ commit }, row) {
        commit(MUTATION_SET_BOOK_ROW_DATA_DETAILS, row.row);
    },
    [ACTION_SET_BOOK_ADD]({commit}, value) {
       commit(MUTATION_SET_BOOK_ADD, value)
    },
    [ACTION_SET_BOOK_ROW_TO_UPDATE]({ commit }, value) {
        commit(MUTATION_SET_BOOK_ROW_TO_UPDATE, value);
    },
    [ACTION_SET_BOOK_UPDATE]({commit}, value) {
        commit(MUTATION_SET_BOOK_UPDATE, value)
    },
};
