$(document).ready(function() {

  $("#startnewgame").click(function() {
    let game_id = $("#joingameid").val();
    let redirect_loc = "/setup/";
    console.log(`Redirecting to ${redirect_loc}`);
    window.location.href = redirect_loc;
  });

  $("#hackydemobutton").click(function() {
    let game_id = $("#joingameid").val();
    let redirect_loc = "/start_demo/" + game_id;
    console.log(`Redirecting to ${redirect_loc}`);
    window.location.href = redirect_loc;
  });

  $("#submitjoingame").click(function() {
    let game_id = $("#joingameid").val();
    let redirect_loc = "/join/" + game_id;
    console.log(`Redirecting to ${redirect_loc}`);
    window.location.href = redirect_loc;
  });
});
