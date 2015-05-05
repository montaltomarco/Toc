package fr.insa_lyon.shifty;

import android.content.Intent;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.RadioGroup;

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
        Intent nextView;
        switch (v.getId()) {
            case R.id.sign_in_button:
                String nom = ((EditText)findViewById(R.id.nom)).getText().toString();
                String prenom = ((EditText)findViewById(R.id.prenom)).getText().toString();
                String age = ((EditText)findViewById(R.id.age)).getText().toString();
                String adresse = ((EditText)findViewById(R.id.adresse)).getText().toString();
                String email = ((EditText)findViewById(R.id.email)).getText().toString();
                String confirmezMdp = ((EditText)findViewById(R.id.passwordConfirm)).getText().toString();
                String mdp = ((EditText)findViewById(R.id.password)).getText().toString();
                String civilite = (findViewById(R.id.radioCivilite)).toString();
                String uri = "http://10.0.2.2:8080/shifty/login/";//a changer par l uri d'inscription
                HttpPostRequest postRequest = new HttpPostRequest();
                postRequest.setValeursPOST("email",email);
                postRequest.setValeursPOST("password", mdp);
                postRequest.setValeursPOST("",nom);
                postRequest.setValeursPOST("",prenom );
                postRequest.setValeursPOST("",civilite);
                postRequest.setValeursPOST("",adresse );
                postRequest.setValeursPOST("",age);
                postRequest.setValeursPOST("",confirmezMdp );
                postRequest.execute(uri);

                nextView = new Intent(getApplicationContext(),LogInActivity.class);
                startActivity(nextView);
                break;
        }
    }


}
