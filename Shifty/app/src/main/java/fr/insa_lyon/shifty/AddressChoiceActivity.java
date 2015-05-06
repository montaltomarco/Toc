package fr.insa_lyon.shifty;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import org.json.JSONArray;
import org.json.JSONObject;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;

/**
 * Created by marcomontalto on 06/05/15.
 */
public class AddressChoiceActivity extends ActionBarActivity {

    private JSONObject response;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_choice_address);
        Bundle b = getIntent().getExtras();

        if(b!=null)
        {
            String value = b.getString("result");

            try {
                response = new JSONObject(value);

                RadioGroup rbtnGrp1 = (RadioGroup)findViewById(R.id.radioGroup_depart);
                for (int i = 0; i < response.getJSONArray("firstAddress").length(); i++) {
                    ((RadioButton) rbtnGrp1.getChildAt(i)).setText(response.getJSONArray("firstAddress").getJSONObject(i).getString("name"));
                    ((RadioButton) rbtnGrp1.getChildAt(i)).setVisibility(View.VISIBLE);
                }

                RadioGroup rbtnGrp2 = (RadioGroup)findViewById(R.id.radioGroup_arrivee);
                for (int i = 0; i < response.getJSONArray("secondAddress").length(); i++) {
                    ((RadioButton) rbtnGrp2.getChildAt(i)).setText(response.getJSONArray("secondAddress").getJSONObject(i).getString("name"));
                    ((RadioButton) rbtnGrp2.getChildAt(i)).setVisibility(View.VISIBLE);
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_choice_address, menu);
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

    public void ButtonOnClickValidate(View v) {
        Intent nextView;
        switch (v.getId()) {
            case R.id.button_NouvelleRecherche:
                //on passe à la vue suivante
                nextView = new Intent(getApplicationContext(),HomeActivity.class); //A changer par une vue avec la liste des addresses proposees
                startActivity(nextView);
                break;
            case R.id.button_Valider:
                String url = "http://10.0.2.2:8080/shifty/route/";
                HttpGetRequest getRequest = new HttpGetRequest();

                try {
                    RadioGroup rbtnGrp1 = (RadioGroup) findViewById(R.id.radioGroup_depart);
                    int radioButtonID = rbtnGrp1.getCheckedRadioButtonId();
                    View radioButton = rbtnGrp1.findViewById(radioButtonID);
                    int idx = rbtnGrp1.indexOfChild(radioButton);
                    JSONObject obj = response.getJSONArray("firstAddress").getJSONObject(idx);
                    getRequest.setNameValuePairs("fromX", obj.getString("lat"));
                    getRequest.setNameValuePairs("fromY", obj.getString("lon"));
                    System.out.println("lat :" + obj.getString("lat"));
                    System.out.println("long :" + obj.getString("lon"));

                    RadioGroup rbtnGrp2 = (RadioGroup) findViewById(R.id.radioGroup_arrivee);
                    int radioButtonID2 = rbtnGrp2.getCheckedRadioButtonId();
                    View radioButton2 = rbtnGrp2.findViewById(radioButtonID2);
                    int idx2 = rbtnGrp2.indexOfChild(radioButton2);
                    JSONObject obj2 = response.getJSONArray("secondAddress").getJSONObject(idx2);
                    getRequest.setNameValuePairs("toX", obj.getString("lat"));
                    getRequest.setNameValuePairs("toY", obj.getString("lon"));
                    System.out.println("lat2 :" + obj2.getString("lat"));
                    System.out.println("long2 :" + obj2.getString("lon"));
                    getRequest.setChoiceActivity(this);
                    getRequest.execute();


                } catch (Exception e) {
                    e.printStackTrace();
                }

                getRequest.setChoiceActivity(this);
                getRequest.execute(url);
                break;
        }
    }

    public void setRoute(String result)
    {
        Intent nextView = new Intent(getApplicationContext(),ItineraireActivity.class);
        Bundle params = new Bundle();
        params.putString("result", result); //Your id
        nextView.putExtras(params); //Put your id to your next Intent
        startActivity(nextView);
    }
}
