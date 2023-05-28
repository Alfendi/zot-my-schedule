// ********* VARIABLE INITIALIZATION & FUNCTION CALLS *********
var professors = ['STAFF', 'IMANI, M', 'EPPSTEIN, D', 'GARETT, R', 'KLEFSTAD, R', 'SHINDLER, M', 'XIE, X', 'MININ, V', 'BIC, L', 'AHMED, I', 'ALFARO, S', 'NAVARRO, E', 'YOUNG, N', 'IHLER, A', 'VAN DER HOEK, A', 'OCHI, D', 'WONG-MA, J', 'CHEN, Q', 'BALDWIN, M', 'JARECKI, S', 'SQUIRE, K', 'IBRAHIM, M', 'KASK, K', 'MJOLSNESS, E', 'HARRIS, I', 'DILLENCOURT, M', 'STEINKUEHLER, C', 'SALEN, K', 'BIETZ, M', 'FEDOROVA, M', 'JONES, J', 'CROOKS, R', 'JORDAN, S', 'GAGO MASAGUE, S', 'KRONE MARTINS, A', 'THORNTON, A', 'BERG, A', 'MAJUMDER, A', 'GASSKO, I', 'ZIV, H', 'DENENBERG, D'];
var courses = ['COMPSCI 175', 'MATH 5B', 'IN4MATX 122A', 'I&C SCI 60', 'COMPSCI 161', 'COMPSCI 112', 'I&C SCI 90', 'I&C SCI 6D', 'I&C SCI 117', 'IN4MATX 175', 'I&C SCI 169', 'MATH 113A', 'I&C SCI 53', 'IN4MATX 122B', 'COMPSCI 171', 'I&C SCI 80', 'I&C SCI 51', 'MATH 134B', 'COMPSCI 151', 'IN4MATX 161', 'MATH 2D', 'COMPSCI 143A', 'I&C SCI 193', 'MATH 132', 'COMPSCI 164', 'MATH 2A', 'COMPSCI 141', 'COMPSCI 134', 'I&C SCI 32', 'MATH 5A', 'I&C SCI 112', 'MATH 175', 'COMPSCI 147', 'MATH 3D', 'MATH 140A', 'I&C SCI 5', 'I&C SCI 141', 'COMPSCI 122B', 'MATH 2B', 'MATH 150', 'MATH 2E', 'MATH 1B', 'MATH 117', 'MATH 147', 'COMPSCI 132', 'I&C SCI 45J', 'I&C SCI 45C', 'MATH 143A', 'I&C SCI 175', 'I&C SCI 122A', 'MATH 164', 'I&C SCI 31', 'COMPSCI 169', 'I&C SCI 143A', 'IN4MATX 134', 'I&C SCI 169A', 'IN4MATX 141', 'IN4MATX 164', 'IN4MATX 117', 'MATH 105A', 'I&C SCI 121', 'I&C SCI 139W', 'MATH 120A', 'I&C SCI 46', 'MATH 169', 'I&C SCI 132', 'IN4MATX H81', 'IN4MATX 169', 'IN4MATX 178', 'MATH 161', 'MATH 10', 'I&C SCI 3', 'MATH 112A', 'I&C SCI 164', 'I&C SCI 122B', 'I&C SCI 178', 'IN4MATX 43', 'I&C SCI 151', 'MATH 171', 'I&C SCI 32A', 'I&C SCI 171', 'IN4MATX 115', 'MATH 3A', 'I&C SCI 33', 'MATH 122B', 'MATH 9', 'IN4MATX 101', 'MATH 134', 'IN4MATX 143A', 'IN4MATX 131', 'MATH 1A', 'MATH 121B', 'I&C SCI 161', 'MATH 121A', 'MATH 134A', 'I&C SCI 134', 'I&C SCI 6B', 'IN4MATX 147', 'MATH 112', 'IN4MATX 151', 'MATH 130A', 'COMPSCI 122A', 'MATH 121', 'IN4MATX 121', 'IN4MATX 112', 'I&C SCI 147', 'MATH 140B', 'MATH 151', 'IN4MATX 132', 'COMPSCI 178', 'MATH 141', 'MATH 122A', 'IN4MATX 171', 'MATH 178', 'MATH 13', 'IN4MATX 133', 'IN4MATX 191A', 'COMPSCI 117', 'I&C SCI H197', 'MATH 192', 'I&C SCI 9', 'COMPSCI 121'];
var courseArray = []; // Declare an empty array to store the course data
var zot_score = 3;  // Zot Score
var dropdown_text = [];

autocomplete(document.getElementById("courseSearchBar"), courses);
autocomplete(document.getElementById("profSearchBar"), professors);

//getStars(zot_score);


// ******** FUNCTION DECLARATIONS ********
function setZot_Score(score) {
  zot_score = score;
}

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
  document.getElementById('inputs').innerHTML += `<li style:"display: flex; flex-direction: row;">
                                                      <div>
                                                        ${"Course: " + courseInput + "<br>" + "Professor: " + profInput}
                                                      </div>
                                                      <button id="deleteButton" onclick="rem(this)">&#x2715</button>
                                                  </li>`;
  document.getElementById('courseSearchBar').value = "";
  document.getElementById('profSearchBar').value = "";
  courseArray.push(courseInput + ", " + profInput);
}

function rem(element) {
  console.log("Before: " + courseArray);
  element.parentElement.remove();
  var courseIndex = courseArray.indexOf(element.parentElement.textContent);
  if (courseIndex > -1) {
    courseArray.splice(courseIndex, 1); // Remove the corresponding value from the courseArray
  }

  console.log("After: " + courseArray);
}

function submitForm() {
  sendFlask(courseArray)
    .then(function(response) {
        console.log(response)
        var zot_score = response.zot_score;
        var dropdown_text = response.dropdown_text;
        getStars(zot_score);

          document.getElementById('inputs2').innerHTML = "";
          for (var i = 0; i < dropdown_text.length; i++) {
            var dropdown_title = dropdown_text[i][0];
            var dropdown_description = dropdown_text[i][1];

            document.getElementById('inputs2').innerHTML += `<button class="collapsible" "> ${dropdown_title}</button>
                                                              <div class="content">
                                                                <p>${dropdown_description}</p>
                                                              </div>`;
            document.getElementById('inputs').innerHTML = "";
        }
      courseArray = [];
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
    })
    .catch(function(error) {
        console.log(error)
    });

}

function getStars(zot_score) {
  var count = 0;

  while (count < zot_score) {
    document.getElementById('zotstars').innerHTML += `<img src="../static/images/zot-star.png" alt="anteater clip art" class="stars">`;
    count++;
  }

  while (count < 5) {
    document.getElementById('zotstars').innerHTML += `<img src="../static/images/empty-zot-star.png" alt="anteater clip art" class="stars">`;
    count++;
  }
}

function showDifficultySuggestions() {
  var x = document.getElementById("altProfToggle").innerText;
  console.log(x);
  if (x === "Show alternative Professors") {
    console.log("TOGGLE");
    document.getElementById("altProfToggle").innerText = "Swapped text!";
  } else {
    document.getElementById("altProfToggle").innerText = "Show alternative Professors";
  }
}

function showQualitySuggestions() {
  var x = document.getElementById("altCourseToggle").innerText;
  if (x === "show alternative Courses") {
    document.getElementById("altCourseToggle").innerText = "Swapped text!";
  } else {
    document.getElementById("altCourseToggle").innerText = "show alternative Courses";
  }
}

function sendFlask(courseArray) {
    return new Promise(function(resolve, reject) {
    var jsonData = JSON.stringify(courseArray);
    console.log(courseArray);

    $.ajax({
      type: 'POST',
      url: '/submitted',
      data: { courseArray: jsonData },
      success: function(response) {
        resolve(response);
      },
      error: function(xhr, status, error) {
        reject(error);
      }
    });
  });
}

