



export function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

export function createToast(type,heading,message){
    let toast = document.getElementById("liveToast");
    if (!type){
      toast.innerHTML = `
      <div class="toast-header">
        <img src="${infoImg}" class="rounded me-2 img img-fluid" width="24px" height="24px" alt="info" />
        <strong class="me-auto">${heading}</strong>
        <small>few seconds ago</small>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="toast"
          aria-label="Close"
        ></button>
      </div>
      <div class="toast-body">${message}</div>
      `;
    }
    if (type === "error"){
      toast.innerHTML = `
      <div class="toast-header">
        <span class="fw-bold text-danger">Eror: X</span>
        <strong class="me-auto text-danger">${heading}</strong>
        <small>Just Now</small>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="toast"
          aria-label="Close"
        ></button>
      </div>
      <div class="toast-body">${message}</div>
      `;
    }
  
    $('#liveToast').toast('show');
  }

export function generateDynamicContent(data,elementId) {
    // Get the container element
    var container = document.getElementById(elementId);
    // console.log(container);
  
    // Create the HTML content
    var html = ``;
    html += `<h2 class="h2 mb-2 text-center">${data.title}</h2>`;
  
    
  
    html += `
    <div class="col-md-4 col-xl-4">
      <div class="card bg-c-green order-card">
        <div class="card-block">
          <h6 class="m-b-20">URLs found</h6>
          <h2 class="text-right">
            <i class="fa fa-link f-left"></i
            ><span class="px-2">${ data.urls.overview.num_urls }</span>
          </h2>
          <p class="m-b-0">
            Urls per body<span class="f-right"
              >${ (data.urls.overview.urls_per_post).toFixed(4) }</span
            >
          </p>
          <p class="m-b-0">
            Unique Urls<span class="f-right"
              >${ data.urls.overview.unique_urls }</span
            >
          </p>
        </div>
      </div>
    </div>
    `
    html += `
    <div class="col-md-4 col-xl-4">
      <div class="card bg-c-yellow order-card">
        <div class="card-block">
          <h6 class="m-b-20">Mentions found</h6>
          <h2 class="text-right">
            <i class="fa fa-quote-left f-left"></i
            ><span class="px-2">${ data.mentions.overview.num_mentions}</span>
          </h2>
          <p class="m-b-0">
            Mentions per body<span class="f-right"
              >${ (data.mentions.overview.mentions_per_post).toFixed(4) }</span
            >
          </p>
          <p class="m-b-0">
            Unique Mentions<span class="f-right"
              >${ data.mentions.overview.unique_mentions }</span
            >
          </p>
        </div>
      </div>
    </div>
    `
    html += `
    <div class="col-md-4 col-xl-4">
      <div class="card bg-c-pink order-card">
        <div class="card-block">
          <h6 class="m-b-20">Questions found</h6>
          <h2 class="text-right">
            <i class="fa fa-question f-left"></i
            ><span class="px-2"
              >${ data.questions.overview.num_question_marks}</span
            >
          </h2>
          <p class="m-b-0">
            Questions per body<span class="f-right"
              >${ (data.questions.overview.question_marks_per_post).toFixed(4)}</span
            >
          </p>
          <p class="m-b-0">
            Unique Questions<span class="f-right"
              >${ data.questions.overview.unique_question_marks }</span
            >
          </p>
        </div>
      </div>
    </div>
    `
    html += `
    <div class="col-md-4 col-xl-4">
      <div class="card bg-c-blue order-card">
        <div class="card-block">
          <h6 class="m-b-20">Hashtags found</h6>
          <h2 class="text-right">
            <i class="fa fa-hashtag f-left"></i
            ><span class="px-2">${ data.hashtags.overview.num_hashtags}</span>
          </h2>
          <p class="m-b-0">
            Hashtags per body<span class="f-right"
              >${ (data.hashtags.overview.hashtags_per_post).toFixed(4)}</span
            >
          </p>
          <p class="m-b-0">
            Unique Hashtags<span class="f-right"
              >${ data.hashtags.overview.unique_hashtags }</span
            >
          </p>
        </div>
      </div>
    </div>
    `
    html += `
    <div class="col-md-4 col-xl-4">
      <div class="card bg-c-green order-card">
        <div class="card-block">
          <h6 class="m-b-20">Numbers found</h6>
          <h2 class="text-right">
            <i class="fa fa-arrow-up f-left"></i
            ><span class="px-2">${ data.numbers.overview.num_numbers}</span>
          </h2>
          <p class="m-b-0">
            Numbers per body<span class="f-right"
              >${(data.numbers.overview.numbers_per_post).toFixed(4)}</span
            >
          </p>
          <p class="m-b-0">
            Unique Numbers<span class="f-right"
              >${data.numbers.overview.unique_numbers }</span
            >
          </p>
        </div>
      </div>
    </div>
    `
  
    html+= `
    <div class="col-md-4 col-xl-4">
      <div class="card bg-c-yellow order-card">
        <div class="card-block">
          <h6 class="m-b-20">Intense Words found</h6>
          <h2 class="text-right">
            <i class="fa fa-repeat f-left"></i
            ><span class="px-2"
              >${ data.intense_words.overview.num_intense_words}</span
            >
          </h2>
          <p class="m-b-0">
            Intense Words per body<span class="f-right"
              >${ (data.intense_words.overview.intense_words_per_post).toFixed(4)}</span
            >
          </p>
          <p class="m-b-0">
            Unique Intense Words<span class="f-right"
              >${ data.intense_words.overview.unique_intense_words }</span
            >
          </p>
        </div>
      </div>
    </div>
    `
  
    // Set the HTML content in the container
    container.innerHTML = html;
  }