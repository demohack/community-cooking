html = `<div id="app">
  <button @click="toggle">toggle</button>
  <h1 v-if="awesome">Vue is awesome!</h1>
  <h1 v-else>Oh no 😢</h1>

  <button @click="increment">increment</button>
  <button @click="decrement">decrement</button>
  <p>Count is: {{ count }}</p>

  <input v-model="text" placeholder="Type here">
  <p ref="p">{{ text }}</p>

  <form @submit.prevent="addTodo">
    <input v-model="newTodo"></form>
    <button>Add Todo</button>
  </form>
  <ul>
    <li v-for="todo in filteredTodos" :key="todo.id">
      <input type="checkbox" v-model="todo.done">
      <span :class="{ done: todo.done }">{{ todo.text }}</span>
      <button @click="removeTodo(todo)">X</button>
    </li>
  </ul>
  <button @click="hideCompleted = !hideCompleted">
    {{ hideCompleted ? 'Show all' : 'Hide completed' }}
  </button>
</div>
`

scriptblock = `
{% block scriptlinks %}
<script src="https://unpkg.com/vue@3"></script>
<script src="{{ url_for('stories.static', filename='api-classes.js') }}"></script>
<script src="{{ url_for('stories.static', filename='ui.js') }}"></script>
<script src="{{ url_for('static', filename='base.js') }}"></script>
<script>
  loadUserSession()
</script>
{% endblock %}
`

let id = 0;

Vue.createApp({
  data() {
    return {
      count: 0,
      text: 'Hello World!',
      awesome: true,
      newTodo: '',
      hideCompleted: false,
      todos: [
        { id: id++, text: 'Learn HTML', done: true },
        { id: id++, text: 'Learn JavaScript', done: true },
        { id: id++, text: 'Learn Vue', done: false }
      ]      
    }
  },
  computed: {
    filteredTodos() {
      return this.hideCompleted
        ? this.todos.filter((t) => !t.done)
        : this.todos
    }
  },
  mounted() {
    this.$refs.p.textContent = "beanstack"
  },
  methods: {
    increment() {
      // update component state
      this.count++
    },

    decrement() {
      // update component state
      this.count--
    },

    toggle() {
      this.awesome = !this.awesome
    },

    addTodo() {
      this.todos.push({ id: id++, text: this.newTodo, done: false })
      this.newTodo = ''
    },

    removeTodo(todo) {
      this.todos = this.todos.filter((t) => t !== todo)
    }
  }
}).mount('#app')
