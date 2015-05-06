package fr.insa_lyon.shifty;

import android.content.Intent;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;


public class HomeActivity extends ActionBarActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_home, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void ButtonOnClickSearch(View v) {
        Intent nextView;
        switch (v.getId()) {
            case R.id.SearchButton:
                //On envoie les données
                String url = "http://10.0.2.2:8080/shifty/coordonnes/";
                HttpGetRequest getRequest = new HttpGetRequest();
                String depart = ((EditText)findViewById(R.id.depart)).getText().toString();
                String arrivee = ((EditText)findViewById(R.id.arrivee)).getText().toString();
                getRequest.setNameValuePairs("firstAddress", depart);
                getRequest.setNameValuePairs("secondAddress", arrivee);
                getRequest.setActivityHome(this);
                getRequest.execute(url);
                break;
            case R.id.SaveButton:
                // Sauvegarder l'itinéraire dasn les favoris
                break;
        }
    }

    public void Dummybutton()
    {
        Intent inte = new Intent(getApplicationContext(),ResultActivity.class);
        startActivity(inte);
    }

    public void setJson(String result){
        //on passe à la vue suivante
        //il faut utiliser result pour avoir les données à passer
        Intent nextView = new Intent(getApplicationContext(),AddressChoiceActivity.class);
        Bundle params = new Bundle();
        params.putString("result", result); //Your id
        nextView.putExtras(params); //Put your id to your next Intent
        startActivity(nextView);
    }
}
