import { setState } from './actions';

const serializers = {
  exclude: list => list.map(String).join(','),
};

const deserializers = {
  exclude: list =>
    (list || '')
      .split(',')
      .map(x => parseInt(x, 10))
      .filter(x => !isNaN(x)),
};

const fields = Object.keys(serializers);

export default class StoreFormSynchronizer {
  constructor(form) {
    this.form = form;
    this.reflectToFormMiddleware = this.reflectToFormMiddleware.bind(this);
  }

  setSubmitForm(submit) {
    this.submit = submit;
  }

  reflectToFormMiddleware(store) {
    return next => action => {
      const result = next(action);
      const state = store.getState();
      let changed = false;

      fields.forEach(field => {
        const oldVal = this.form.get(field);
        const newVal = serializers[field](state[field]);

        if (oldVal !== newVal) {
          this.form.set(field, newVal);
          changed = true;
        }
      });

      if (changed) {
        this.submit(true);
      }

      return result;
    };
  }

  reflectToStore(store) {
    const state = store.getState();
    const changes = {};

    fields.forEach(field => {
      console.log('reflect to store', state, this.form.get(field));
      console.trace();

      const oldVal = serializers[field](state[field]);
      const newSerializedVal = deserializers[field](this.form.get(field));
      const newVal = serializers[field](newSerializedVal);

      if (oldVal !== newVal) {
        changes[field] = newSerializedVal;
      }
    });

    if (Object.keys(changes).length) {
      store.dispatch(setState(Object.assign({}, state, changes)));
    }
  }
}
