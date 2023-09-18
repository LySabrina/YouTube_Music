document.addEventListener("yt-navigate-start", () => {
  if (checkIfExist()) {
    addButton();
  }
});

function checkIfExist() {
  const downloadButton = document.getElementById("yt-music-download");
  if (downloadButton == null) {
    return true;
  }
  return false;
}

function addButton() {
  const actions = document.getElementById("actions");

  const helloButton = document.createElement("button");
  helloButton.setAttribute("id", "yt-music-download");
  helloButton.setAttribute(
    "class",
    "yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading "
  );
  helloButton.textContent = "YouTube_Music Download";

  // helloButton.addEventListener("click", async () => {
  //   const fetchPromise = fetch("http://localhost:8080/BookDetails/1");
  //   fetchPromise
  //     .then((response) => {
  //       console.log(response);
  //     })
  //     .catch((error) => {
  //       console.log(`YOUTUBE_MUSIC ERROR: ${error}`);
  //     });
  // });
  helloButton.addEventListener('click',  (event)=>{
    // const apiURL = "https://randomuser.me/api/";
    event.preventDefault();
    const apiURL = "http://localhost:8080/"
    fetch(apiURL).then((response)=>{
      console.log(response.data)
    }).catch((error)=>{
      console.log(error)
    })
  })
  actions.append(helloButton);
}
