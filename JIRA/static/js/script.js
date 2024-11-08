document.addEventListener("DOMContentLoaded", function () {
  // Initialize Sortable.js on the kanban board
  const taskBoxes = document.querySelectorAll(".project-detail");
  const options = {
      group: "shared",
      animation: 150,
      setData: function (dataTransfer, dragEl) {
          dataTransfer.setData("text", dragEl.id);
      },
      onEnd: function (evt) {
          const taskId = parseInt(evt.item.id);
          const newState = evt.to.id;
          updateTaskStatus(taskId, newState);
          evt.to.classList.remove("drag-over");

      },
  };

  // Add draggable attribute to tasks in each state box
  taskBoxes.forEach((taskBox) => {
      const tasks = taskBox.querySelectorAll(".task");
      tasks.forEach((task) => {
          task.setAttribute("draggable", true);
          task.addEventListener("dragstart", function (e) {
              console.log('dragging')
              e.dataTransfer.setData("text", e.target.id);
          });
          task.addEventListener("dragend", function (e) {
              console.log("dragend");
          });
      });

      // Add dragover and dragleave event listeners to each task box
      taskBox.addEventListener("dragover", function (e) {
          e.preventDefault();
          taskBox.classList.add("drag-over");
      });

      taskBox.addEventListener("dragleave", function (e) {
          taskBox.classList.remove("drag-over");
      });


      // Initialize Sortable for each state box
      new Sortable(taskBox, options);
  });


});

function updateTaskStatus(taskId, newState) {
  // Send an API request to update the task status
  fetch(`/tasks/${taskId}/edit`, {
      method: 'PUT',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({taskId, newState}),
  })
      .then(response => {
          if (response.ok) {
              // Task status updated successfully
              console.log('Task status updated successfully');
              location.reload();
          } else {
              // Error handling
              console.error('Error updating task status');
          }
      })
      .catch(error => {
          console.error('API request error:', error);
      });
}

function editTask(taskId) {
  // Send an API request to update the task status
  fetch(`/tasks/${taskId}/edit`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({taskId}),
  })
      .then(response => {
          if (response.ok) {
              // Task status updated successfully
              console.log('Task status updated successfully');
              location.reload();
          } else {
              // Error handling
              console.error('Error updating task status');
          }
      })
      .catch(error => {
          console.error('API request error:', error);
      });
}

function saveTask(taskId) {
  // Send an API request to update the task status
  fetch(`/tasks/${taskId}/save`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          taskId,
          name: document.getElementById('name').value,
          description: document.getElementById('description').value,
          active: document.getElementById('active').value,
          priority: document.getElementById('priority').value,
          status: document.getElementById('status').value,
          date_start: document.getElementById('date_start').value,
          date_end: document.getElementById('date_end').value,
          project_id: parseInt(document.getElementById('project_id').value),
      }),
  })
      .then(response => {
          if (response.ok) {
              // Task status updated successfully
              console.log('Task status updated successfully');
              location.reload();
          } else {
              // Error handling
              console.error('Error updating task status');
          }
      })
      .catch(error => {
          console.error('API request error:', error);
      });
}

function renderTaskList(tasks) {
  // Select the task list elements in the DOM
  const todoList = document.getElementById('todo');
  const inProgressList = document.getElementById('in-progress');
  const doneList = document.getElementById('done');

  // Clear the task lists
  todoList.innerHTML = '';
  inProgressList.innerHTML = '';
  doneList.innerHTML = '';

  let todoCount = 0;
  let inProgressCount = 0;
  let doneCount = 0;

  // Loop through the array of tasks
  tasks.forEach(state => {
      // Create a new task element and populate it with the task data

      const task = state[Object.keys(state)[0]];
      const taskElement = `
          <div onClick="window.location.href='/tasks/${task.id}'"
               class="task ${task.priority === 'high' ? 'task-high' : task.priority === 'medium' ? 'task-med' : 'task-low'}"
               id="${task.id}">
              <div class="d-flex justify-content-between align-items-center">
                  <p>
                      ${task.name}
                  </p>
                  <a class="stopPropagation btn btn-primary btn-sm" style="margin-bottom: 10px"
                     href="/tasks/delete/${task.id}">
                      Delete
                  </a>
              </div>

              <div>
                  <span>Description:</span>${task.description || ''}
              </div>
              <div>
                  <span>Due Date:</span> ${task.date_end}
              </div>
              <div>
                  <span>Priority:</span> ${task.priority}
              </div>
          </div>`;

      // Append the new task element to the appropriate task list
      if (Object.keys(state)[0] == 'todo') {
          todoList.innerHTML += taskElement;
          todoCount++;
      } else if (Object.keys(state)[0] == 'in-progress') {
          inProgressList.innerHTML += taskElement;
          inProgressCount++;
      } else if (Object.keys(state)[0] == 'done') {
          doneList.innerHTML += taskElement;
          doneCount++;
      }
  });

  // Update the task count
  document.getElementsByClassName('todo task-length')[0].textContent = `To Do (${todoCount})`;
  document.getElementsByClassName('in-progress task-length')[0].textContent = `In Progress (${inProgressCount})`;
  document.getElementsByClassName('done task-length')[0].textContent = `Done (${doneCount})`;

}

(function () {
  async function searchTask(value) {
      return fetch('/tasks/search', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              keyword: value,
          }),
      })
          .then(response => response.json())
          .then(data => {
              renderTaskList(data)
          })
          .catch(error => {
              console.error('AJAX request error:', error);
          });
  }

  const renderItem = (item) => (item.description
      ? `<a class="tippy-child" href="/tasks/${item.id}">
         <strong>${item.name}</strong>
         <span>${item.desc}</span>
         </a>`
      : `<a class="tippy-child" href="/tasks/${item.id}">
         <strong>${item.name}</strong>
         </a>`)
  const renderList = (list) => list.map(item => renderItem(item))
      .reduce((start, value) => start + value, '')


  const searchInput = document.getElementById("searchInput")
  const searchBar = document.getElementById("searchBar")
  const tippy = document.getElementById("tippy")
  const loading = document.getElementById("loading")

  tippy.style.display = "none"
  loading.style.display = "none"
  let timerId;
  let focus;

  searchInput.onkeyup = (e) => {
      clearTimeout(timerId)
      const value = searchInput.value;
      loading.style.display = "block"

      if (!value) {
          tippy.style.display = "none"
          loading.style.display = "none"
          return;
      }
      timerId = setTimeout(async () => {
          searchTask(value).then(data => {
              if (!focus || !data || data.length === 0) {
                  tippy.style.display = "none"
                  loading.style.display = "none"
                  return;
              }
              tippy.style.display = "flex"
              tippy.innerHTML = `
                  <span>Tìm thấy ${data.length} kết quả với từ khóa <strong>"${value}"</strong></span>
                  <div>
                      ${renderList(data)}
                  </div>`
          }).catch(() => {
              tippy.style.display = "flex"
              tippy.innerHTML = `<span>Không tìm thấy kết quả với từ khóa <strong>"${value}"</strong></span>`
          }).finally(() => {
              loading.style.display = "none"
          })

      }, 500)
  }
  searchInput.onfocus = () => focus = true
  searchBar.onblur = () => {
      focus = false
      tippy.style.display = "none"
      loading.style.display = "none"
  }
})()

let users_link = document.getElementById('users-link');
let tasks_link = document.getElementById('task-link');

if (tasks_link) {
    if (window.location.pathname === '/users/') {
        tasks_link.classList.remove('active');
        users_link.classList.add('active');
    } else {
        tasks_link.classList.add('active');
        users_link.classList.remove('active');
    }
}
