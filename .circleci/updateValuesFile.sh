set -e

INFRA_MODULES_DIR='infrastructure-modules/services/dtx-helm-charts'
ROOT_DIR=/root/project

cd $ROOT_DIR

PROJECT_COMMON_PATH='did-spec/did-alliance-spec'

if [[ "$CIRCLE_BRANCH" == "circleci-project-setup" ]]; then
  echo "On develop branch. Deploying to dev."
  VALUES_FILE_PATH="infrastructure-live/dev/us-west-2/dev/$PROJECT_COMMON_PATH/env/dev"
  RAFAY_PROJECT='dev'
else
  echo "Did not find release tag or master branch, so skipping deploy."
  exit 0
fi

echo export RCTL_PROJECT=$RAFAY_PROJECT >> $BASH_ENV

printf "\n<=============== Setting image tag on values file ===============>\n"
newImageTag=$CIRCLE_SHA1 yq eval -i  '.image.tag= env(newImageTag)' $VALUES_FILE_PATH/values.yaml

printf "\n<=============== Push changes to Bitbucket ===============>\n"
cd "$VALUES_FILE_PATH"
git config user.name $GIT_USERNAME
git config user.email $GIT_EMAIL

git add .
git diff-index --quiet HEAD || (git commit -m "CircleCI Bot: Updated image tag of '$RAFAY_WORLOAD_NAME' to $CIRCLE_SHA1" &&  git push --set-upstream origin develop)



printf "\n<=============== Create Helm Chart Zip file ===============>\n"
echo $INFRA_MODULES_DIR
cd $ROOT_DIR/$INFRA_MODULES_DIR
pwd
tar -cvzf dtx-helm-chart.tgz dtx-common-helm-chart


printf "\n<=============== Setting properties in workload spec file ===============>\n"
EKS_CLUSTER_NAME='rafay-dev-eks-cluster'
EKS_NAMESPACE=$(yq eval '.namespace'  $ROOT_DIR/$VALUES_FILE_PATH/values.yaml)
#RAFAY_WORKLOAD_NAME=$(yq eval '.name'  $ROOT_DIR/$VALUES_FILE_PATH/values.yaml)
HELM_CHART_FILEPATH=$ROOT_DIR/$INFRA_MODULES_DIR/dtx-helm-chart.tgz
HELM_VALUES_FILEPATH=$ROOT_DIR/$VALUES_FILE_PATH/values.yaml


clusters=$EKS_CLUSTER_NAME yq eval -i '.clusters= env(clusters) ' rafay-workload-spec-template.yaml
namespace=$EKS_NAMESPACE yq eval -i '.namespace= env(namespace) ' rafay-workload-spec-template.yaml
name=$RAFAY_WORLOAD_NAME yq eval -i '.name= env(name) ' rafay-workload-spec-template.yaml
payload=$HELM_CHART_FILEPATH yq eval -i '.payload= env(payload) ' rafay-workload-spec-template.yaml
values=$HELM_VALUES_FILEPATH yq eval -i '.values= env(values) ' rafay-workload-spec-template.yaml

cat rafay-workload-spec-template.yaml

