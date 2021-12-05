$(document).ready(function() {
  console.log("I ran!")
  $("#submitjoingame").click(function() {
    let game_id = $("#joingameid").val();
    let redirect_loc = "/play/" + game_id;
    console.log(`Redirecting to ${redirect_loc}`);
    window.location.href = redirect_loc;
  });
});
