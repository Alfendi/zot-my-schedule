// ********* VARIABLE INITIALIZATION & FUNCTION CALLS *********
var courses = ["ICS 46", "ICS 45C", "COMPSCI 161", "COMPSCI 117", "COMPSCI 117"];
var professors = ["Michael Shindler", "Richard Pattis", "Alex Thornton"];
var courseArray = []; // Declare an empty array to store the course data

autocomplete(document.getElementById("courseSearchBar"), courses);
autocomplete(document.getElementById("profSearchBar"), professors);

// ******** FUNCTION DECLARATIONS ********
function show() {
  document.getElementById('sidebar').classList.toggle('active');
}

function autocomplete(inp, arr) {
  var currentFocus;

  inp.addEventListener("input", function (e) {
    var a, b, i, val = this.value;

    closeAllLists();
    if (!val) { return false; }
    currentFocus = -1;

    a = document.createElement("DIV");
    a.setAttribute("id", this.id + "autocomplete-list");
    a.setAttribute("class", "autocomplete-items");

    this.parentNode.appendChild(a);

    for (i = 0; i < arr.length; i++) {

      if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {

        b = document.createElement("DIV");

        b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
        b.innerHTML += arr[i].substr(val.length);

        b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";

        b.addEventListener("click", function (e) {

          inp.value = this.getElementsByTagName("input")[0].value;

          closeAllLists();
        });
        a.appendChild(b);
      }
    }
  });

  inp.addEventListener("keydown", function (e) {
    var x = document.getElementById(this.id + "autocomplete-list");
    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {

      currentFocus++;

      addActive(x);
    } else if (e.keyCode == 38) { //up


      currentFocus--;

      addActive(x);
    } else if (e.keyCode == 13) {

      e.preventDefault();
      if (currentFocus > -1) {

        if (x) x[currentFocus].click();
      }
    }
  });
  function addActive(x) {

    if (!x) return false;

    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);

    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {

    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }

  document.addEventListener("click", function (e) {
    closeAllLists(e.target);
  });
}


function add() {
  let courseInput = document.getElementById('courseSearchBar').value;
  let profInput = document.getElementById('profSearchBar').value;
  document.getElementById('inputs').innerHTML += `<li>${courseInput + profInput}<span onclick="rem(this)">X</span></li>`;
  document.getElementById('courseSearchBar').value = "";
  document.getElementById('profSearchBar').value = "";
  courseArray.push(courseInput + ",\t" + profInput);
}

function rem(element) {
  element.parentElement.remove();
  var courseIndex = courseArray.indexOf(element.parentElement.textContent);
  if (courseIndex > -1) {
    courseArray.splice(courseIndex, 1); // Remove the corresponding value from the courseArray
  }
}

function submitForm() {
  console.log("Submitting form")
  for (var i = 0; i < courseArray.length; i++) {
    var userInput = courseArray[i];
    document.getElementById('inputs2').innerHTML += `<button class="collapsible">${userInput}</button>
                                                      <div class="content">
                                                        <p>hello</p>
                                                        <p>hello</p>
                                                        <p>hello</p>
                                                      </div>`;
  }
  var coll = document.getElementsByClassName("collapsible");
  var i;

  for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
      this.classList.toggle("active");
      var content = this.nextElementSibling;
      
      if (content.style.maxHeight) {
        content.style.maxHeight = null;
      } else {
        content.style.maxHeight = content.scrollHeight + "px";
      }
    });
  }
}