from requests import JSONDecodeError
from src.app.models import HTPInput, HTPOutput, Usage, MethodList, AnalysisOutput
from fastapi import FastAPI, HTTPException, status


def create_app(model):
    app = FastAPI(
        title = "HTP Test",
        description = "A simple web application that uses the House-Tree-Person test to analyze an image.",
    )

    @app.post("/v1/predict", response_model=HTPOutput, status_code=status.HTTP_200_OK)
    async def predict(data: HTPInput):
        try:
            assert data.language in ["en", "zh"], "Language must be either 'en' or 'zh'."
            result = model.workflow(
                image_path=data.image_path,
                language=data.language
            )
            result = HTPOutput(
                usage=Usage(
                    total_tokens=result["usage"]["total"],
                    prompt_tokens=result["usage"]["prompt"],
                    completion_tokens=result["usage"]["completion"]
                ),
                overall=AnalysisOutput(
                    feature=result["overall"]["feature"],
                    analysis=result["overall"]["analysis"],
                ),
                house=AnalysisOutput(
                    feature=result["house"]["feature"],
                    analysis=result["house"]["analysis"],
                ),
                tree=AnalysisOutput(
                    feature=result["tree"]["feature"],
                    analysis=result["tree"]["analysis"],
                ),
                person=AnalysisOutput(
                    feature=result["person"]["feature"],
                    analysis=result["person"]["analysis"],
                ),
                merge=result["merge"],
                final=result["final"],
                signal=result["signal"],
                classification=result["classification"],
                fix_signal=result["fix_signal"]
            )

            return result
        
        except JSONDecodeError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @app.get("/v1/methods", status_code=status.HTTP_200_OK)
    async def list_methods():
        return MethodList(
            method=["predict"]
        )
        
    return app