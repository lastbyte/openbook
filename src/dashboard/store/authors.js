import {
    ACTION_SET_AUTHOR_TABLE_DATA,
    ACTION_SET_AUTHOR_ADD,
    ACTION_SET_AUTHOR_UPDATE,
    ACTION_SET_AUTHOR_ROW_DATA_DETAILS,
    ACTION_SET_AUTHOR_ROW_TO_UPDATE
} from '~/store-config/action.types';
import {
    MUTATION_SET_AUTHOR_TABLE_DATA,
    MUTATION_SET_AUTHOR_ADD,
    MUTATION_SET_AUTHOR_UPDATE,
    MUTATION_SET_AUTHOR_ROW_DATA_DETAILS,
    MUTATION_SET_AUTHOR_ROW_TO_UPDATE
} from '~/store-config/mutation.types';

export const state = () => ({
    authorOptions: [],
    authorTable: {
        items: [],
        totalRows: 0,
        filter: '',
        perPage: '10',
        currentPage: 1,
    },
    rowToUpdate : {},
    addAuthor: {
        id : null,
        name : '',
        age : null,
        description : ''

    },
    updateAuthor: {},
});

export const mutations = {
    [MUTATION_SET_AUTHOR_TABLE_DATA](state, value) {
        state.authorTable = { ...state.authorTable, ...value };
    },
    [MUTATION_SET_AUTHOR_ROW_DATA_DETAILS](state, row) {
        row.toggleDetails();
        state.authorTable.items.splice(row.index, 1, row.item);
    },
    [MUTATION_SET_AUTHOR_ADD](state, value) {
        state.addAuthor = { ...state.addAuthor, ...value };
    },
    [MUTATION_SET_AUTHOR_ROW_TO_UPDATE](state, value) {
        state.rowToUpdate = { ...value };
    },
    [MUTATION_SET_AUTHOR_UPDATE](state, value) {
        state.updateAuthor = { ...state.updateAuthor, ...value };
    },
};

export const actions = {
    [ACTION_SET_AUTHOR_TABLE_DATA]({ commit }, value) {
        commit(MUTATION_SET_AUTHOR_TABLE_DATA, value);
    },
    [ACTION_SET_AUTHOR_ROW_DATA_DETAILS]({ commit }, row) {
        commit(MUTATION_SET_AUTHOR_ROW_DATA_DETAILS, row.row);
    },
    [ACTION_SET_AUTHOR_ADD]({ commit }, value) {
        commit(MUTATION_SET_AUTHOR_ADD, value);
    },
    [ACTION_SET_AUTHOR_ROW_TO_UPDATE]({ commit }, value) {
        commit(MUTATION_SET_AUTHOR_ROW_TO_UPDATE, value);
    },
    [ACTION_SET_AUTHOR_UPDATE]({ commit }, value) {
        commit(MUTATION_SET_AUTHOR_UPDATE, value);
    },
};
