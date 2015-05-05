package fr.insa_lyon.shifty;

import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;

import java.net.URL;
import java.util.ArrayList;
import java.util.List;


public class SignInActivity extends ActionBarActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_in);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_sign_in, menu);
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

    public void ButtonOnClickSign(View v)
    {
        switch (v.getId()) {
            case R.id.sign_in_button:
                String nom = ((EditText)findViewById(R.id.nom)).getText().toString();
                String prenom = ((EditText)findViewById(R.id.prenom)).getText().toString();
                String uri = "http://10.0.2.2:8080/shifty/login/";//a changer par l uri d'inscription
                HttpPostRequest postRequest = new HttpPostRequest();
                postRequest.setValeursPOST("nickname",nom);
                postRequest.setValeursPOST("password", prenom);
                postRequest.execute(uri);
                //Exemple d'appel de getRequest
               /* HttpGetRequest getRequest = new HttpGetRequest();
                String url = "http://10.0.2.2:8080/shifty/coordonnes/";
                String address1 = ((EditText)findViewById(R.id.adresse1)).getText().toString();
                String address2 = ((EditText)findViewById(R.id.adresse2)).getText().toString();
                getRequest.setNameValuePairs("firstAddress", adress1);
                getRequest.setNameValuePairs("firstAddress", adress2);
                getRequest.execute(url);*/
                break;
        }
    }


}
