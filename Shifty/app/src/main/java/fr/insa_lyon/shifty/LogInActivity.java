package fr.insa_lyon.shifty;

import android.content.Intent;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;


public class LogInActivity extends ActionBarActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_log_in);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_log_in, menu);
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

    /* Button handler */
    public void ButtonOnClickLog(View v) {
        Intent nextView;
        switch (v.getId()) {
            case R.id.connexionButton:
                //On envoie les données
                String email = ((EditText)findViewById(R.id.email)).getText().toString();
                String password = ((EditText)findViewById(R.id.password)).getText().toString();
                String uri = "http://10.0.2.2:8080/shifty/login/";
                HttpPostRequest postRequest = new HttpPostRequest();
                postRequest.setValeursPOST("nickname",email);
                postRequest.setValeursPOST("password", password);
                postRequest.execute(uri);
                //on passe à la vue suivante
                nextView = new Intent(getApplicationContext(),HomeActivity.class);
                startActivity(nextView);
                break;
            case R.id.inscriptionButton:
                nextView = new Intent(getApplicationContext(), SignInActivity.class);
                startActivity(nextView);
                break;
        }
    }
}
