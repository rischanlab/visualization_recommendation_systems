/**
 * @author Tarique
 */
package edu.uiuc.zenvisage.zql.functions;

import java.util.List;

import edu.uiuc.zenvisage.data.remotedb.VisualComponent;
import edu.uiuc.zenvisage.data.remotedb.VisualComponentList;
import edu.uiuc.zenvisage.zql.AxisVariable;
import edu.uiuc.zenvisage.zql.AxisVariableScores;

/**
 * @author tarique
 *
 */
public interface D {
	public  AxisVariableScores  execute(VisualComponentList f1, VisualComponentList f2, List<List<AxisVariable>> axisVariables);
	public double calculateDistance(VisualComponent v1, VisualComponent v2);
}
