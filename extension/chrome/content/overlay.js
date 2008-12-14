Components.utils.import("resource://firenomics/reporter.js");

function fnLoad() {
  var appcontent = window.document.getElementById("appcontent");
  if (appcontent) {
    if (!appcontent.firenomicsInited) {
      appcontent.firenomicsInited = true;
      appcontent.addEventListener("DOMContentLoaded", function(event) { fnInit(event); }, false);
    }
  }
}

function fnInit(event) {
  var win = new XPCNativeWrapper(event.originalTarget, "top");

  if (win.location.href.match(FIRENOMICS_URL + "/profile")) {
    fnRenderProfilePage(win);
    return;
  }
}

function fnGotoProfilePage() {
  alert('going to profile page');
  openUILinkIn(FirenomicsReporter.FIRENOMICS_URL + "/profile/foo", "tab");
}

function fnRenderProfilePage(win) {
  alert('rendering profile page');
}

function fnSubmit() {
  alert('submitting stuffs');
  FirenomicsReporter.submit();
}

fnLoad();
